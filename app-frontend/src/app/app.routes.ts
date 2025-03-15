import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';

export const routes: Routes = [
    {path: '', component: LoginComponent},
    {path: 'admin-dashboard', loadComponent: () => import('./admin-dashboard/admin-dashboard.component').then(m => m.AdminDashboardComponent) },
    {path: 'dorm-bookings', loadComponent: () => import('./dorm-bookings/dorm-bookings.component').then(m => m.DormBookingsComponent) },
    {path: 'login', loadComponent: () => import('./login/login.component').then(m => m.LoginComponent) }, // Explicitly define the login route
    {path: 'create-account', loadComponent: () => import('./create-account/create-account.component').then(m => m.CreateAccountComponent) }, // Explicitly define the create account route
    {path: 'account-info', loadComponent: () => import('./account-info/account-info.component').then(m => m.AccountInfoComponent) }, // Explicitly define the account info route
    {path: '**', redirectTo: ''}, // Redirect to login for any unknown routes


];
