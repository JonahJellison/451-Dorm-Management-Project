import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { AuthService } from '../auth-service/auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, HttpClientModule, RouterModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  username: string | null = null;
  password: string | null = null;
  errorMessage: string | null = null;

  constructor(
    private http: HttpClient,
    private router: Router,
    private authservice: AuthService,
    private route: ActivatedRoute
  ) {}
  
  ngOnInit(): void {
    // Check for error parameter in URL
    this.route.queryParams.subscribe(params => {
      if (params['error'] === 'invalid_token') {
        this.errorMessage = 'Invalid or expired verification link. Please try logging in or request a new verification email.';
      }
    });
  }

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
        if (error.error && typeof error.error === 'string' && 
          error.error.includes("Account not activated")) {
          this.errorMessage = "Account not activated. Please check your email for confirmation.";
        } else {
          this.errorMessage = 'Login failed. Please try again.';
        }
      }
    );
  }
}
