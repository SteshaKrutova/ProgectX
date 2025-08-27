from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User, Service  # Импортируем модели
from app.forms import LoginForm, RegistrationForm
from app.decorators import client_required, contractor_required
from flask_mail import Message  # Импортируем объект Message из Flask-Mail

# Blueprint для аутентификации
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('auth/login.html', form=form, title='Вход')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data, 
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        if current_user.is_authenticated:
            # Если регистрация из панели клиентов - вернуться туда
            if request.form.get('from_clients_page'):
                return redirect(url_for('main.clients_list'))
            return redirect(url_for('main.dashboard'))
        else:
            return redirect(url_for('auth.login'))
            
    return render_template('auth/register.html', form=form, title='Регистрация')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Blueprint для основных страниц
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'client':
        return render_template('client/dashboard.html', title='ЛК Клиента')
    else:
        return render_template('contractor/dashboard.html', title='ЛК Заказчика')

@main_bp.route('/clients')
@login_required
@contractor_required
def clients_list():
    clients = User.get_all_clients()
    return render_template('contractor/clients.html', 
                         clients=clients, 
                         title='Список клиентов')

@main_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@contractor_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Нельзя удалить себя
    if user.id == current_user.id:
        flash('Нельзя удалить собственный аккаунт', 'danger')
        return redirect(url_for('main.clients_list'))
    
    db.session.delete(user)
    db.session.commit()
    flash(f'Пользователь {user.username} удален', 'success')
    return redirect(url_for('main.clients_list'))

# Маршрут для страницы составления отчетов
@main_bp.route('/reports')
@login_required
@contractor_required
def reports():
    return render_template('contractor/reports.html', title="Составление отчетов")

# Маршрут для обработки отправки формы отчетов
@main_bp.route('/generate_report', methods=['POST'])
@login_required
@contractor_required
def generate_report():
    report_type = request.form.get('report_type')
    date_range = request.form.get('date_range', '').strip()
    
    if report_type == 'custom' and not date_range:
        flash('Для пользовательского отчета необходимо указать диапазон дат.', 'error')
        return redirect(url_for('main.reports'))
    
    # Логика генерации отчета (можно дополнить)
    flash(f'Отчет типа "{report_type}" успешно сформирован.', 'success')
    return redirect(url_for('main.reports'))

# Маршрут для страницы управления услугами
@main_bp.route('/manage_services')
@login_required
@client_required
def manage_services():
    # Получаем список услуг текущего пользователя
    services = Service.query.filter_by(user_id=current_user.id).all()
    return render_template('client/manage_services.html', title="Управление услугами", services=services)

# Маршрут для изменения статуса услуги (вкл/выкл)
@main_bp.route('/toggle_service/<int:service_id>', methods=['POST'])
@login_required
@client_required
def toggle_service(service_id):
    # Получаем услугу по ID
    service = Service.query.get_or_404(service_id)
    
    # Проверяем, принадлежит ли услуга текущему пользователю
    if service.user_id != current_user.id:
        flash('У вас нет доступа к этой услуге.', 'danger')
        return redirect(url_for('main.manage_services'))
    
    # Меняем статус услуги
    service.is_active = not service.is_active
    db.session.commit()
    
    # Формируем сообщение для отправки
    status = "включена" if service.is_active else "выключена"
    subject = f"Услуга {service.name} {status}"
    body = f"""
    Здравствуйте!

    Статус услуги "{service.name}" был изменён.
    Текущий статус: {status}.
    """

    # Отправляем письмо
    try:
        msg = Message(subject, recipients=[current_user.email])  # Email пользователя
        msg.body = body
        current_app.extensions['mail'].send(msg)  # Используем current_app для доступа к mail
        flash(f'Статус услуги "{service.name}" изменен. Уведомление отправлено на почту.', 'success')
    except Exception as e:
        flash(f'Не удалось отправить уведомление на почту: {str(e)}', 'warning')

    return redirect(url_for('main.manage_services'))

# Обработчик для загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))