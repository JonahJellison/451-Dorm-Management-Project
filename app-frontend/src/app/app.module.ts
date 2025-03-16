import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { AppRoutingModule } from './app-routing.module';
import { LoginComponent } from './login/login.component';
import { CreateAccountComponent } from './create-account/create-account.component';

@NgModule({
    declarations: [
        // ...existing declarations...
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule, // Add FormsModule to imports
        LoginComponent,
        CreateAccountComponent,
        // ...existing imports...
    ],
    providers: [],
})
export class AppModule { }
