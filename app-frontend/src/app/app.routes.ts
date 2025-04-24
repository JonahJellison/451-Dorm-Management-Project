import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';

export const routes: Routes = [
    {path: '', component: LoginComponent},
    {path: 'admin-dashboard', loadComponent: () => import('./admin-dashboard/admin-dashboard.component').then(m => m.AdminDashboardComponent) },
    {path: 'dorm-bookings', loadComponent: () => import('./dorm-bookings/dorm-bookings.component').then(m => m.DormBookingsComponent) },
    {path: 'login', loadComponent: () => import('./login/login.component').then(m => m.LoginComponent) }, // Explicitly define the login route
    {path: 'create-account', loadComponent: () => import('./create-account/create-account.component').then(m => m.CreateAccountComponent) }, // Explicitly define the create account route
    {path: 'account-info', loadComponent: () => import('./account-info/account-info.component').then(m => m.AccountInfoComponent) }, // Explicitly define the account info route
    {path: 'email-confirmation-success', loadComponent: () => import('./email-confirmation-success/email-confirmation-success.component').then(m => m.EmailConfirmationSuccessComponent) },
    {path: 'confirm-email/:uidb64/:token', redirectTo: 'email-confirmation-success'},
    {path: 'forgot-password', loadComponent: () => import('./forgot-password/forgot-password.component').then(m => m.ForgotPasswordComponent) },
    {path: 'reset-password/:token/:uid', loadComponent: () => import('./reset-password/reset-password.component').then(m => m.ResetPasswordComponent) },
    {path: '**', redirectTo: ''}, // Redirect to login for any unknown routes
];
