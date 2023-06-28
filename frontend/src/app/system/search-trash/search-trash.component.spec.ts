import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchTrashComponent } from './search-trash.component';

describe('SearchTrashComponent', () => {
  let component: SearchTrashComponent;
  let fixture: ComponentFixture<SearchTrashComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SearchTrashComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SearchTrashComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
