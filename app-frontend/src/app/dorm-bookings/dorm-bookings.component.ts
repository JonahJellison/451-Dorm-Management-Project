import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-dorm-bookings',
  templateUrl: './dorm-bookings.component.html',
  styleUrls: ['./dorm-bookings.component.css'],
  imports: [CommonModule, FormsModule, HttpClientModule],
  standalone: true
})

export class DormBookingsComponent {
constructor(private http: HttpClient) {}

selectedBuilding: string = '';
selectedRoomType: string = '';
selectedPriceRange: string = '';

duncan_img: string = "/duncan_dunn.jpg";
global_img: string = "/global_scholars.jpg";
honors_img: string = "/honors.jpg";
northside_img: string = "/northside.jpg";

selected_dorms: Room[] = [];
selectedRoomForBooking: Room | null = null;
showBookingPopup: boolean = false;
requestRoommate: boolean = false;
roommateStudentId: string = '';
leaseDuration: number = 6; // Default to 6 months

getDormImage(dormName: string): string {
  console.log('Getting image for dorm:', dormName);
  switch(dormName.toLowerCase()) {
    case 'duncan dunn':
      return this.duncan_img;
    case 'global scholars':
      return this.global_img;
    case 'honors hall':
      return this.honors_img;
    case 'northside':
      return this.northside_img;
    default:
      return ''; // Default image or empty string if no match
  }
}

applyFilters() {
  console.log('Filtering with:', {
    building: (this.selectedBuilding !== '' ? this.selectedBuilding : 'All'),
    roomType: (this.selectedRoomType !== '' ? this.selectedRoomType : 'All'),
    priceRange: (this.selectedPriceRange !== '' ? this.selectedPriceRange : 'All')
  });

  const filters = {
    building: (this.selectedBuilding !== '' ? this.selectedBuilding : 'All'),
    roomType: (this.selectedRoomType !== '' ? this.selectedRoomType : 'All'),
    priceRange: (this.selectedPriceRange !== '' ? this.selectedPriceRange : 'All')
  }
  
  interface RoomResponse {
    rooms: Room[];
  }
  
  this.http.get<RoomResponse>('http://127.0.0.1:8000/api/fetch_dormroom_data', { params: filters })
    .subscribe((response: RoomResponse) => {
      this.selected_dorms = response.rooms;
      console.log('Filtered dorms:', this.selected_dorms);
    });
}

openBookingPopup(room: Room) {
  this.selectedRoomForBooking = room;
  this.showBookingPopup = true;
  this.requestRoommate = false;
  this.roommateStudentId = '';
  this.leaseDuration = 6; // Reset to default when opening popup
}

closeBookingPopup() {
  this.showBookingPopup = false;
  this.selectedRoomForBooking = null;
}

submitBooking() {
  if (!this.selectedRoomForBooking) return;
  
  const bookingData = {
    room_id: this.selectedRoomForBooking.room_id,
    request_roommate: this.requestRoommate,
    roommate_student_id: this.requestRoommate ? this.roommateStudentId : null,
    lease_duration: this.leaseDuration
  };
  
  console.log('Submitting booking:', bookingData);
  
  // Here you would send the booking data to your API
  this.http.post('http://127.0.0.1:8000/api/book_room', bookingData)
    .subscribe(
      (response) => {
        console.log('Booking successful:', response);
        alert('Room booked successfully!');
        this.closeBookingPopup();
      },
      (error) => {
        console.error('Booking error:', error);
        alert('Error booking room. Please try again.');
      }
    );
}

}

interface Room {
  room_id: number;
  dorm_name: string;
  room_number: string;
  capacity: number;
  has_AC: boolean;
  has_private_bath: boolean;
  cost_per_month: number;
}
