import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService, JWT_NAME } from 'src/app/shared/services/auth.service';
import { User } from 'src/app/shared/model/user.model';
import { GlobalConfig } from 'src/app/global';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  form1: FormGroup = new FormGroup({});
  form2: FormGroup=new FormGroup({});
  isOpen = false;
  trueMessage = 'Incorrect your data';
  resMessage = '';
  formUser=true;

  constructor(
    private router: Router,
    private auth: AuthService
  ) { }

  ngOnInit(): void {
    this.form1 = new FormGroup({
      email: new FormControl(null, [Validators.required, Validators.email]),
      password: new FormControl(null, [Validators.required, Validators.minLength(6)]),
    });
    this.form2 = new FormGroup({
      emailEx: new FormControl(null, [Validators.required, Validators.email]),
      nameEx: new FormControl(null, [Validators.required]),
      passwordEx: new FormControl(null, [Validators.required, Validators.minLength(6)]),
    });
  }

  get login(): FormControl {
    return this.form1.get('email') as FormControl;
  }

  get password(): FormControl {
    return this.form1.get('password') as FormControl;
  }

  get nameEx(): FormControl {
    return this.form2.get('nameEx') as FormControl;
  }

  get loginEx(): FormControl {
    return this.form2.get('emailEx') as FormControl;
  }

  get passwordEx(): FormControl {
    return this.form2.get('passwordEx') as FormControl;
  }

  onLogin() {
    if (this.form1.valid) {
      const login = this.login.value;
      const passwd = this.password.value;
      const user = new User(login, passwd);
      this.auth.loginUser(user)
        .subscribe({
          next: (res) => {
            localStorage.setItem(JWT_NAME,res["access_token"]);
            this.router.navigate(['/system', 'about-us']);
            GlobalConfig.flagMenu1 = false;
            GlobalConfig.flagMenu2 = true;
            GlobalConfig.flagMenu3 = true;
          },
          error: (err) => {
            this.resMessage = err["error"]["detail"];
            if (this.resMessage == this.trueMessage) {
              this.isOpen = true;
            }
          }
        });
    }
  }

  onLoginEx() {
    if (this.form2.valid) {
      const login = this.loginEx.value;
      const name = this.nameEx.value;
      const passwd = this.passwordEx.value;
      this.auth.loginExpert({
        "login": login,
        "name": name,
        "password": passwd,
      })
        .subscribe({
          next: (res) => {
            localStorage.setItem(JWT_NAME,res["access_token"]);
            this.router.navigate(['/expert', 'requests']);
          },
          error: (err) => {
            this.resMessage = err["error"]["detail"];
            if (this.resMessage == this.trueMessage) {
              this.isOpen = true;
            }
          }
        });
    }
  }

  close() {
    this.isOpen = false;
    this.form1.reset();
  }

  open(event: any) {
    if (event.target.checked == true) {
      this.formUser = false;
    }
  }
}
