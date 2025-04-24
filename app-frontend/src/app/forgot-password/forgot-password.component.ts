import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [FormsModule, HttpClientModule, RouterModule, CommonModule],
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent {
  identifier: string = '';
  isSubmitting: boolean = false;
  successMessage: string = '';
  errorMessage: string = '';

  constructor(private http: HttpClient) {}

  requestPasswordReset(): void {
    this.isSubmitting = true;
    this.successMessage = '';
    this.errorMessage = '';

    // Validate the input
    if (!this.identifier.trim()) {
      this.errorMessage = 'Please enter your email or student ID';
      this.isSubmitting = false;
      return;
    }

    // Determine if the identifier is an email or student ID
    const isEmail = this.identifier.includes('@');
    
    const payload = {
      identifier: this.identifier,
      type: isEmail ? 'email' : 'student_id'
    };

    this.http.post('http://localhost:8000/api/request-password-reset', payload)
      .subscribe(
        (response: any) => {
          this.isSubmitting = false;
          this.successMessage = 'Password reset instructions have been sent to your email.';
          this.identifier = ''; // Clear the form
        },
        (error) => {
          this.isSubmitting = false;
          if (error.error && typeof error.error === 'string') {
            this.errorMessage = error.error;
          } else {
            this.errorMessage = 'An error occurred. Please try again later.';
          }
          console.error('Password reset request error:', error);
        }
      );
  }
}
