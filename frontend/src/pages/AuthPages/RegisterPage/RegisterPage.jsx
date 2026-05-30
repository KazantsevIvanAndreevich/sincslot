import React, {useEffect, useRef, useState} from 'react';
import {Link} from 'react-router-dom';
import styles from '../Auth.module.css';
import {authService} from "../../../services/authService";
import {useNavigate} from "react-router-dom";
import {toast} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Register = () => {
  const navigate = useNavigate();

  const inputRefs = useRef([]);
  useEffect(() => {
    inputRefs.current[0]?.focus();
  }, []);

  const [formData, setFormData] = useState({
    name: '',
    address: '',
    email: '',
    phone: '',
    password: '',
    repeatPassword: ''
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const {name, value} = e.target;

    let newValue = value;
    if (name === "phone") {
      if (newValue === "7") {
        newValue = "+7";
      }

      if (newValue === "+7") {
        newValue = "+7";
      }

      newValue = newValue.replace(/[^\d+]/g, "");
    }

    setFormData((prev) => {
      const newFormData = {...prev, [name]: newValue};

      setErrors((prevErrors) => {
        const newErrors = {...prevErrors};

        newErrors[name] = validateField(name, newValue, newFormData);

        if ((name === 'password' || name === 'repeatPassword') && newFormData.repeatPassword) {
          newErrors.repeatPassword = validateField(
            'repeatPassword',
            newFormData.repeatPassword,
            newFormData
          );
        }

        return newErrors;
      });

      return newFormData;
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!isFormValid) return;

    try {
      const result = await authService.register(formData);

      // Сохраняем токен
      localStorage.setItem("accessToken", result.accessToken);

      console.log('Регистрация успешна:', formData);

      // Перенаправляем на главную
      navigate("/settings");

    } catch (error) {
      console.error("Ошибка регистрации:", error);

      const serverError = error?.response?.data?.error;

      // Если сервер прислал строку — выводим её, иначе fallback
      toast.error(serverError || "Ошибка регистрации. Попробуйте позже");
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === 'Enter') {
      e.preventDefault();

      const nextInput = inputRefs.current[index + 1];
      if (nextInput) nextInput.focus();
    }
  };

  const validateField = (name, value, currentFormData) => {
    switch (name) {
      case 'name':
        return value.trim() ? '' : 'Введите название организации';
      case 'address':
        return value.trim() ? '' : 'Введите адрес организации';
      case 'email': {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(value) ? '' : 'Введите корректный email';
      }
      case 'phone': {
        const phoneRegex = /^\+?\d{11}$/;
        return phoneRegex.test(value.replace(/\s+/g, '')) ? '' : 'Введите корректный телефон';
      }
      case 'password': {
        const errors = [];

        if (value.length < 6) {
          errors.push('Минимум 6 символов');
        }
        if (!/[A-Z]/.test(value)) {
          errors.push('Хотя бы одна заглавная буква (A–Z)');
        }
        if (!/[a-z]/.test(value)) {
          errors.push('Хотя бы одна строчная буква (a–z)');
        }
        if (!/[!@#$%^&*()_+\-=]/.test(value)) {
          errors.push('Хотя бы один спецсимвол: !@#$%^&*()_+-=');
        }

        return errors.join(', ');
      }
      case 'repeatPassword':
        return value === currentFormData.password ? '' : 'Пароли не совпадают';
      default:
        return '';
    }
  };

  // Проверка, есть ли ошибки или незаполненные поля
  const isFormValid =
    Object.values(errors).every((err) => !err) &&
    Object.values(formData).every((val) => val.trim() !== '');

  const fields = [
    {label: 'Название организации', name: 'name', type: 'text', placeholder: 'Введите название вашей организации'},
    {label: 'Адрес', name: 'address', type: 'text', placeholder: 'Введите адрес вашей организации'},
    {label: 'Email', name: 'email', type: 'email', placeholder: 'example@mail.ru'},
    {label: 'Телефон', name: 'phone', type: 'tel', placeholder: '+7 XXX XXX XX XX'},
    {label: 'Пароль', name: 'password', type: 'password', placeholder: 'Придумайте надежный пароль'},
    {label: 'Повторите пароль', name: 'repeatPassword', type: 'password', placeholder: 'Повторите ваш пароль'}
  ];

  return (
    <div className={styles.authContainer}>
      <div className={styles.authCard}>
        <div className={styles.authHeader}>
          <h2>Регистрация в SyncSlot</h2>
          <p>Создайте новый аккаунт</p>
        </div>

        <form onSubmit={handleSubmit} className={styles.authForm}>
          {fields.map((field, index) => (
            <div key={field.name} className={styles.formGroup}>
              <label htmlFor={field.name}>{field.label}</label>
              <input
                type={field.type}
                id={field.name}
                name={field.name}
                value={formData[field.name]}
                onChange={handleChange}
                placeholder={field.placeholder}
                required
                ref={(el) => (inputRefs.current[index] = el)}
                onKeyDown={(e) => handleKeyDown(e, index)}
                autoComplete={
                  field.name === 'email'
                    ? 'email'
                    : field.name === 'password' || field.name === 'repeatPassword'
                      ? 'new-password'
                      : undefined
                }
              />
              {errors[field.name] && (
                <span className={styles.error}>{errors[field.name]}</span>
              )}
            </div>
          ))}

          <button
            type="submit"
            className={`${styles.btn} ${styles.btnPrimary} ${styles.btnFull}`}
            disabled={!isFormValid} // кнопка неактивна, пока есть ошибки
          >
            Зарегистрироваться
          </button>

          <div className={styles.authLinks}>
            <span>Уже есть аккаунт?</span>
            <Link to="/login" className={styles.authLink}>
              Войти
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
