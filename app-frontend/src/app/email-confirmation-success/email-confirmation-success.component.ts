import { Component, OnInit } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-email-confirmation-success',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './email-confirmation-success.component.html',
  styleUrls: ['./email-confirmation-success.component.css']
})
export class EmailConfirmationSuccessComponent implements OnInit {
  constructor(private router: Router) {}

  ngOnInit(): void {
    // As the user is automatically redirected here from the backend
    // we can assume the account activation was successful
    // The account is already activated by the backend endpoint
  }

  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }
}
