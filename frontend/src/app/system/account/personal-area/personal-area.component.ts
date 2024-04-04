import { Component, OnInit } from '@angular/core';
import { UserService } from 'src/app/shared/services/user.service';
import { Router } from '@angular/router';
import { GlobalConfig } from 'src/app/global';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import { matchpassword } from 'src/app/auth/matchpassword.validator';

@Component({
  selector: 'app-personal-area',
  templateUrl: './personal-area.component.html',
  styleUrls: ['./personal-area.component.css']
})

export class PersonalAreaComponent implements OnInit {

  email: string = "";
  amount_garbage:number=0;
  form1: FormGroup=new FormGroup({});
  form2: FormGroup=new FormGroup({});
  flagM=true;
  flagL=false;
  flagP=false;
  isOpen2 = false;
  trueMessageL='Email already exist';
  flag1=true;
  flag2=false;
  trueMessageP='The old password has been entered';
  resMessage='';
  isOpen1 = false;

  constructor(private userService: UserService, private router: Router) { }
  ngOnInit(): void {
    this.userService.getUser()
      .subscribe((response: any) => {
        this.amount_garbage=response["amount_garbage"];
        this.email=response["email"];
      });
      this.form1 = new FormGroup({
        password: new FormControl(null, [Validators.required, Validators.minLength(6)]),
        confirmPassword: new FormControl(null)
      },
      {
        validators:matchpassword
      });
      this.form2 = new FormGroup({
        email: new FormControl(null, [Validators.required, Validators.email]),
      });
  }

  deleteUser()
  {
    this.userService.deleteUser()
    .subscribe((response: any) => {
      this.router.navigate(['/system','about-us']);
      GlobalConfig.flagMenu1=this.flag1;
      GlobalConfig.flagMenu2=this.flag2;
      GlobalConfig.flagMenu3=this.flag2;
      GlobalConfig.t="";
    });
  }

  get login(): FormControl {
    return this.form2.get('email') as FormControl;
  }

  get password(): FormControl {
    return this.form1.get('password') as FormControl;
  }

  cPassword()
  {
    this.flagM=false;
    this.flagP=true;
  }

  cLogin()
  {
    this.flagM=false;
    this.flagL=true;
  }

  changePassword()
  {
    const passwd=this.password.value;
    this.userService.updatePassword({
      "password":passwd
    })
    .subscribe({
      next:(res)=>{
        this.form1.reset();
        this.flagM=true;
        this.flagP=false;
        GlobalConfig.t="";
        this.router.navigate(['login']);
      },
      error:(err)=>{
        this.resMessage=err["error"]["detail"];
       if(this.resMessage==this.trueMessageP)
       {
        this.isOpen1=true;
        this.resMessage='';
       }
      }
    })
  }

  changeLogin()
  {
    const login= this.login.value;
    this.userService.updateLogin({
      "email":login
    })
    .subscribe({
      next:(res)=>{
      this.form2.reset();
      this.flagM=true;
      this.flagL=false;
      GlobalConfig.t="";
      this.router.navigate(['login']);
      },
      error:(err)=>{
        this.resMessage=err["error"]["detail"];
       if(this.resMessage==this.trueMessageL)
       {
        this.isOpen2=true;
        this.resMessage='';
       }
      }
    });
  }

  close1()
  {
    this.isOpen1=false;
    this.form1.reset();
  }

  close2()
  {
    this.isOpen2=false;
    this.form2.reset();
  }

}


