import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-account',
  standalone: true,
  imports: [ReactiveFormsModule, HttpClientModule],
  templateUrl: './create-account.component.html',
  styleUrls: ['./create-account.component.css']
})
export class CreateAccountComponent implements OnInit {
  registerForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private router: Router  // Inject Router
  ) {}

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      fullname: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      studentid: ['', Validators.required],
      newPassword: ['', Validators.required],
      confirmPassword: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      return;
    }
    if (this.registerForm.value.newPassword !== this.registerForm.value.confirmPassword) {
      alert('Passwords do not match.');
      return;
    }
    const payload = {
      fullname: this.registerForm.value.fullname,
      email: this.registerForm.value.email,
      studentid: this.registerForm.value.studentid,
      password: this.registerForm.value.newPassword
    };
    const url = 'http://localhost:8000/api/register/';
    this.http.post(url, payload).subscribe(
      (response) => {
        console.log('Registration successful:', response);
        // Redirect to /login on success:
        this.router.navigate(['/login']);
      },
      (error) => {
        console.error('Registration error:', error);
      }
    );
  }
}
