from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.decorators import client_required, contractor_required

# blueprint для аутентификации
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['get', 'post'])
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
        flash('неверное имя пользователя или пароль', 'danger')
    return render_template('auth/login.html', form=form, title='вход')

@auth_bp.route('/register', methods=['get', 'post'])
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
            # если регистрация из панели клиентов - вернуться туда
            if request.form.get('from_clients_page'):
                return redirect(url_for('main.clients_list'))
            return redirect(url_for('main.dashboard'))
        else:
            return redirect(url_for('auth.login'))
            
    return render_template('auth/register.html', form=form, title='регистрация')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# blueprint для основных страниц
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'client':
        return render_template('client/dashboard.html', title='лк клиента')
    else:
        return render_template('contractor/dashboard.html', title='лк заказчика')

@main_bp.route('/clients')
@login_required
@contractor_required
def clients_list():
    clients = User.get_all_clients()
    return render_template('contractor/clients.html', 
                         clients=clients, 
                         title='список клиентов')

@main_bp.route('/delete_user/<int:user_id>', methods=['post'])
@login_required
@contractor_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # нельзя удалить себя
    if user.id == current_user.id:
        flash('нельзя удалить собственный аккаунт', 'danger')
        return redirect(url_for('main.clients_list'))
    
    db.session.delete(user)
    db.session.commit()
    flash(f'пользователь {user.username} удален', 'success')
    return redirect(url_for('main.clients_list'))

# обработчик для загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
