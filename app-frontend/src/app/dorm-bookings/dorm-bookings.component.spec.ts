import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DormBookingsComponent } from './dorm-bookings.component';

describe('DormBookingsComponent', () => {
  let component: DormBookingsComponent;
  let fixture: ComponentFixture<DormBookingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DormBookingsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DormBookingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
