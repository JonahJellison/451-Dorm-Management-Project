import { Component, OnInit } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [FormsModule, HttpClientModule, RouterModule, CommonModule],
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.css']
})
export class ResetPasswordComponent implements OnInit {
  token: string | null = null;
  uid: string | null = null;
  password: string = '';
  confirmPassword: string = '';
  isSubmitting: boolean = false;
  passwordMismatch: boolean = false;
  successMessage: string = '';
  errorMessage: string = '';

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Get token and uid from route parameters
    this.route.paramMap.subscribe(params => {
      this.token = params.get('token');
      this.uid = params.get('uid');
      
      if (!this.token || !this.uid) {
        this.errorMessage = 'Invalid password reset link.';
      }
    });
  }

  resetPassword(): void {
    this.isSubmitting = true;
    this.successMessage = '';
    this.errorMessage = '';

    // Check if passwords match
    if (this.password !== this.confirmPassword) {
      this.passwordMismatch = true;
      this.errorMessage = 'Passwords do not match.';
      this.isSubmitting = false;
      return;
    }

    this.passwordMismatch = false;

    if (!this.token || !this.uid) {
      this.errorMessage = 'Invalid password reset link.';
      this.isSubmitting = false;
      return;
    }

    const payload = {
      token: this.token,
      uid: this.uid,
      new_password: this.password
    };

    this.http.post('http://localhost:8000/api/reset-password', payload)
      .subscribe(
        (response: any) => {
          this.isSubmitting = false;
          this.successMessage = 'Your password has been successfully reset.';
          
          // Redirect to login page after 3 seconds
          setTimeout(() => {
            this.router.navigate(['/login']);
          }, 3000);
        },
        (error) => {
          this.isSubmitting = false;
          if (error.error && typeof error.error === 'string') {
            this.errorMessage = error.error;
          } else {
            this.errorMessage = 'An error occurred. Please try again later.';
          }
          console.error('Password reset error:', error);
        }
      );
  }
}
