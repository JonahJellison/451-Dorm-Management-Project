import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../auth-service/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string | null = null;
  password: string | null = null;

  constructor(private http: HttpClient,private router: Router, private authservice: AuthService) {}
  

  login(): void {
    // validate
    if (!this.username || !this.password) {
      console.error('Student ID and Password must be provided');
      return;
    }
    if (this.username.length < 5 || this.password.length < 5) {
      console.error('Student ID or Password must be 5 or more characters each');
      return;
    }
    
    // create data to send to the backend
    const payload = {
      id: this.username,
      password: this.password
    };

    this.http.post('http://localhost:8000/api/login', payload).subscribe(
      (response: any) => {
        console.log('Login successful:', response);
        this.authservice.setUser(this.username!); // Student ID
        localStorage.setItem('studentId', this.username!);
        this.router.navigate(['/dorm-bookings']);
      },
      (error) => {
        console.error('Login error:', error);
      }
    );
  }
}
