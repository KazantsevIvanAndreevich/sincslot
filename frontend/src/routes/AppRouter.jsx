import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "../pages/AuthPages/LoginPage/LoginPage.jsx";
import RegisterPage from "../pages/AuthPages/RegisterPage/RegisterPage.jsx";
import ForgotPasswordPage from "../pages/AuthPages/ForgotPasswordPage/ForgotPasswordPage.jsx";
import HomePage from "../pages/HomePage/HomePage.jsx";
import SchedulePage from "../pages/SchedulePage/SchedulePage.jsx";
import ServicesPage from "../pages/ServicesPage/ServicesPage.jsx";
import ClientBookingPage from "../pages/ClientBookingPage/ClientBookingPage.jsx";
import BookingDetailsPage from "../pages/BookingDetailsPage/BookingDetailsPage.jsx";
import BookingConfirmationPage from "../pages/BookingConfirmationPage/BookingConfirmationPage.jsx";
import CompanySettingsPage from "../pages/CompanySettingsPage/CompanySettingsPage.jsx";
import MyBookingsAuthPage from "../pages/MyBookingsAuthPage/MyBookingsAuthPage.jsx";
import MyBookingsPage from "../pages/MyBookingsPage/MyBookingsPage.jsx";
import PrivateRoute from "./PrivateRoute.jsx";

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Главная страница */}
        <Route path="/" element={<HomePage />} />

        {/* Авторизация */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />

        {/* Услуги */}
        <Route path="/services" element={<ServicesPage />} />

        {/*Только для авторизованных */}
        {/* Расписание */}
        <Route
          path="/schedule"
          element={
            <PrivateRoute>
              <SchedulePage />
            </PrivateRoute>
          }
        />
        {/* Настройки компании */}
        <Route
          path="/settings"
          element={
            <PrivateRoute>
              <CompanySettingsPage/>
            </PrivateRoute>
          }
        />

       {/*Запись клиента*/}
       <Route path="/booking" element={<ClientBookingPage />} />

       {/*Детали записи и подтверждение*/}
       <Route path="/booking-details" element={<BookingDetailsPage />} />
       <Route path="/booking-confirmation" element={<BookingConfirmationPage />} />

       <Route path="/my-bookings-auth" element={<MyBookingsAuthPage />} />
      <Route path="/my-bookings" element={<MyBookingsPage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default AppRouter;
