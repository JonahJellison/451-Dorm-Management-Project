import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-dorm-bookings',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './dorm-bookings.component.html',
  styleUrl: './dorm-bookings.component.css'
})
export class DormBookingsComponent {

selectedBuilding: string = '';
selectedRoomType: string = '';
selectedPriceRange: string = '';

applyFilters() {
  // Implement your filtering logic here
  console.log('Filtering with:', {
    building: this.selectedBuilding,
    roomType: this.selectedRoomType,
    priceRange: this.selectedPriceRange
  });
  
  // Fetch or filter rooms based on selections
}
}
