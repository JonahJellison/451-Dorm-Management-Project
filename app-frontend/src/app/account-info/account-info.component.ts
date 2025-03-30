import { Component } from '@angular/core';

@Component({
  selector: 'app-account-info',
  standalone: true,
  imports: [],
  templateUrl: './account-info.component.html',
  styleUrl: './account-info.component.css'
})
export class AccountInfoComponent {
  infoView: boolean = true;
  bookingView: boolean = false;
  id: string = "John Doe";
}
