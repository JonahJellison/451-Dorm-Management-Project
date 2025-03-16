import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  username: string | null = null;
  password: string | null = null;

  login() {
    if (this.username === null || this.password === null) {
      console.error('Student ID must be provided');
      return;
    }
    if (this.username.length < 5 || this.password.length < 5) {
      console.error('Student ID or Password must be 5 or more characters each');
      return;
    }
    console.log('Logging in with', this.username, this.password);
  }
}
