import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create-account',
  standalone: true,
  imports: [ReactiveFormsModule, HttpClientModule, CommonModule, RouterModule],
  templateUrl: './create-account.component.html',
  styleUrls: ['./create-account.component.css']
})
export class CreateAccountComponent implements OnInit {
  registerForm!: FormGroup;
  passwordMismatch = false;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      fullname: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      studentid: ['', Validators.required],
      newPassword: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required]
    });
  }

  onSubmit(): void {
    this.passwordMismatch = false;
    console.log('Form submitted');
    if (this.registerForm.invalid) {
      // Mark all fields as touched to display validation errors
      Object.keys(this.registerForm.controls).forEach(key => {
        const control = this.registerForm.get(key);
        control?.markAsTouched();
      });
      return;
    }
    
    if (this.registerForm.value.newPassword !== this.registerForm.value.confirmPassword) {
      this.passwordMismatch = true;
      return;
    }
    
    const payload = {
      fullname: this.registerForm.value.fullname,
      email: this.registerForm.value.email,
      studentid: this.registerForm.value.studentid,
      password: this.registerForm.value.newPassword
    };
    
    const url = 'http://localhost:8000/api/register';
    this.http.post(url, payload).subscribe(
      (response) => {
        console.log('Registration successful:', response);
        alert('Account created successfully!');
        this.router.navigate(['/login']);
      },
      (error) => {
        console.error('Registration error:', error);
        alert('Registration failed. Please try again.');
      }
    );
  }
}
