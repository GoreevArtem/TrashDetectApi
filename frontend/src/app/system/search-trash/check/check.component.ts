import { Component, Input } from '@angular/core';
import { GlobalConfig } from 'src/app/global';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.css']
})
export class CheckComponent {
  adress: string = "";
  sentAdress: string = '';
  date: any;
  next=false;
  
 file= GlobalConfig.path.split('@#%#@');
 
  setValues(e:any) {
    if(e.isTrusted==true)
    {
      this.sentAdress = this.adress;
      GlobalConfig.adress=this.adress;
      localStorage.setItem('street', this.sentAdress);
      this.next=true;
      console.log(this.file);
    }
  }

}


