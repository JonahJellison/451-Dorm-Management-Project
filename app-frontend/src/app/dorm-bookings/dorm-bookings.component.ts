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

duncan_img: string = "public\\duncan_dunn.jpg";
global_img: string = "public\\global_scholars.jpg";
honors_img: string = "public\\honors.jpg";
northside_img: string = "public\\northside.jpg";

selected_dorms: Room[] = [];

getDormImage(dormName: string): string {
  switch(dormName.toLowerCase()) {
    case 'duncan dunn':
      return this.duncan_img;
    case 'global scholars':
      return this.global_img;
    case 'honors':
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

}

interface Room {
  capacity: number;
  cost_per_month: number;
  created_at: string;
  dorm_id : number;
  has_AC: boolean;
  has_private_bath: boolean;
  is_available: boolean;
  room_id: number;
  room_number: string;
}
