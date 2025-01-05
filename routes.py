from flask import render_template, redirect, url_for, request, flash, Blueprint
from flask_login import login_user, login_required, current_user, logout_user
from . import db, bcrypt
from .models import User
from .forms import LoginForm, RegisterForm, AddUserForm, EditUserForm

main = Blueprint('main', __name__)

# Route untuk halaman utama (root)
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    else:
        return redirect(url_for('main.login'))

# Route untuk halaman login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

# Route untuk halaman registrasi
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# Route untuk logout
@main.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.login'))

# Route untuk dashboard
@main.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=10)  # Pagination
    return render_template('dashboard.html', users=users)

# Route untuk menghapus user
@main.route('/delete_user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    # Cek apakah admin atau user yang login adalah dirinya sendiri
    if user.id == current_user.id or current_user.is_admin:
        db.session.delete(user)
        db.session.commit()
        flash('User has been deleted', 'success')
    else:
        flash('You do not have permission to delete this user.', 'danger')
    return redirect(url_for('main.dashboard'))

# Route untuk menambahkan user
@main.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('User added successfully', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_user.html', form=form)

# Route untuk mengedit user
@main.route('/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)

    # Cek apakah admin atau user yang login adalah dirinya sendiri
    if current_user.id != user.id and not current_user.is_admin:
        flash('You do not have permission to edit this user.', 'danger')
        return redirect(url_for('main.dashboard'))

    form = EditUserForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data

        # Memperbarui password jika diperlukan
        if form.password.data:
            user.password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        db.session.commit()

        flash('User updated successfully', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('edit_user.html', form=form, user=user)
