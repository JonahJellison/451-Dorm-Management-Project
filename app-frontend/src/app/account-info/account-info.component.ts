import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-account-info',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './account-info.component.html',
  styleUrls: ['./account-info.component.css']
})
export class AccountInfoComponent implements OnInit {
  // Fields for user details.
  studentId: string = '';
  name: string = '';
  email: string = '';

  // Fields for additional student info.
  phone: string = '';
  homeAddress: string = '';
  emergencyContact: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    // Retrieve the student ID from localStorage.
    const cachedId = localStorage.getItem('studentId');
    if (cachedId) {
      this.studentId = cachedId;
      
      // Fetch basic user details (student_id, name, email).
      this.http
        .get<{ student_id: string; name: string; email: string }>(
          `http://localhost:8000/api/fetch_student_data?studentId=${this.studentId}`
        )
        .subscribe(
          (data) => {
            this.studentId = data.student_id;
            this.name = data.name;
            this.email = data.email;
          },
          (error) => {
            console.error('Error fetching student data:', error);
          }
        );

      // Fetch additional student info (phone, home address, emergency contact).
      this.http
        .get<{ phone_number: string; home_address: string; emergency_contact: string }>(
          `http://localhost:8000/api/student_info?studentId=${this.studentId}`
        )
        .subscribe(
          (data) => {
            this.phone = data.phone_number || '';
            this.homeAddress = data.home_address || '';
            this.emergencyContact = data.emergency_contact || '';
          },
          (error) => {
            console.error('Error fetching student info:', error);
          }
        );
    } else {
      console.error('No student ID found in localStorage');
    }
  }

  // Called when the form is submitted.
  updateAllInfo(): void {
    // Payload for updating user details.
    const userPayload = {
      user_id: this.studentId,
      name: this.name,
      email: this.email
    };

    // Payload for updating additional student info.
    const studentInfoPayload = {
      studentId: this.studentId,
      phone_number: this.phone,
      home_address: this.homeAddress,
      emergency_contact: this.emergencyContact
    };

    // Use forkJoin to perform both HTTP POST requests concurrently.
    forkJoin({
      userUpdate: this.http.post('http://localhost:8000/api/update_student_info', userPayload),
      studentInfoUpdate: this.http.post('http://localhost:8000/api/student_info', studentInfoPayload)
    }).subscribe({
      next: (response) => {
        console.log('Both updates successful:', response);
        alert('User information updated successfully.');
      },
      error: (error) => {
        console.error('Error updating information:', error);
        alert('Error updating information.');
      }
    });
  }
}
