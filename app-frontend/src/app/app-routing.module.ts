import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { EmailConfirmationSuccessComponent } from './email-confirmation-success/email-confirmation-success.component';
import { CreateAccountComponent } from './create-account/create-account.component';

const routes: Routes = [
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'login', component: LoginComponent },
    { path: 'email-confirmation-success', component: EmailConfirmationSuccessComponent },
    { path: 'confirm-email/:uidb64/:token', redirectTo: '/email-confirmation-success', pathMatch: 'full' },
    { path: 'create-account', component: CreateAccountComponent }, // Explicitly define the create account route
    { path: 'forgot-password', loadChildren: () => import('./forgot-password/forgot-password.component').then(m => m.ForgotPasswordComponent) },
    { path: 'reset-password/:token/:uid', loadChildren: () => import('./reset-password/reset-password.component').then(m => m.ResetPasswordComponent) }
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
