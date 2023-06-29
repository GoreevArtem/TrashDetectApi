import { Component } from '@angular/core';
import { classTrash } from './classTrash';
import { RequestUserService } from 'src/app/shared/services/requestUser.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-no-photo',
  templateUrl: './no-photo.component.html',
  styleUrls: ['./no-photo.component.css']
})
export class NoPhotoComponent {
  modalT:string='';
  longStr="";
  isOpen = false;
  adress="";

  constructor(private request:RequestUserService, private router:Router){}

  classesTrash:classTrash[]=[
    {'nameClass':'пластик'},
    {'nameClass':'крупногабаритный мусор'},
    {'nameClass':'стекло'},
    {'nameClass':'ветки'},
    {'nameClass':'металл'},
    {'nameClass':'бумага'},
    {'nameClass':'картон'},
    {'nameClass':'мусорные мешки'},
];

   getVal(event:any){
    this.modalT=event.target.value;
    this.longStr+=this.modalT+';';
   }
 
   done()
   {
    const adress = this.adress;
    const class_trash = this.longStr;
    console.log(class_trash);
    this.request.createRequest({
      "address":adress,
      "class_trash":class_trash
    })
      .subscribe({
        next: (res) => {
          console.log(res);
          this.isOpen=true;
        }
      });
   }

   close()
   {
    this.isOpen=false;
    this.router.navigate(['/system','account','applications']);
   }
}
