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
    this.longStr+=this.modalT+', ';
   }
 
   done()
   {
    let dl=this.longStr.length;
    let tmp="";
    for(let i=0;i<dl;i++)
    {
      if(i==dl-2)
      {
        tmp+='.';
      }
      else
      {
        tmp+=this.longStr[i];
      }
    }
    const adress = this.adress;
    const class_trash = tmp;
    this.request.createRequest({
      "address":adress,
      "class_trash":class_trash
    })
      .subscribe({
        next: (res) => {
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
