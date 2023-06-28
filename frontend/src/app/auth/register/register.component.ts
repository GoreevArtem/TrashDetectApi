import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from 'src/app/shared/services/auth.service';
import { matchpassword } from '../matchpassword.validator';
import { matchpasswordEx } from '../matchpasswordEx.validator';
import { User } from 'src/app/shared/model/user.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})

export class RegisterComponent implements OnInit {
  form1: FormGroup = new FormGroup({});
  form2: FormGroup=new FormGroup({});
  formUser = true;

  constructor(private auth: AuthService, private router: Router) { }

  ngOnInit(): void {
    this.form1 = new FormGroup({
      name: new FormControl(null, [Validators.required]),
      email: new FormControl(null, [Validators.required, Validators.email]),
      password: new FormControl(null, [Validators.required, Validators.minLength(6)]),
      confirmPassword: new FormControl(null),
    },{ validators: matchpassword});

    this.form2 = new FormGroup({
      nameEx: new FormControl(null, [Validators.required]),
      emailEx: new FormControl(null, [Validators.required, Validators.email]),
      passwordEx: new FormControl(null, [Validators.required, Validators.minLength(6)]),
      confirmPasswordEx: new FormControl(null),
      regOperEx: new FormControl(null, [Validators.required])
    },{ validators: matchpasswordEx});
  }

  get login(): FormControl {
    return this.form1.get('email') as FormControl;
  }
  get name(): FormControl {
    return this.form1.get('name') as FormControl;
  }
  get password(): FormControl {
    return this.form1.get('password') as FormControl;
  }


  get regOperEx(): FormControl {
    return this.form2.get('regOperEx') as FormControl;
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

  onSingup() {
    if (this.form1.valid) {
        const name = this.name.value;
        const login = this.login.value;
        const passwd = this.password.value;
        const user = new User(login, passwd, name);
        this.auth.signUpUser(user)
          .subscribe((response: any) => {
            this.form1.reset();
            this.router.navigate(['login']);
          });
    }
  }

  onSingupEx()
  {
    if (this.form2.valid) {
      const name = this.nameEx.value;
      const reg_oper = this.regOperEx.value;
      const login = this.loginEx.value;
      const passwd = this.passwordEx.value;

      this.auth.signUpExpert({
        "login": login,
        "name": name,
        "password": passwd,
        "region_operator": reg_oper
      }).subscribe((response: any) => {
        this.form1.reset();
        this.router.navigate(['login']);
      })
    }
  }

  open(event: any) {
    if (event.target.checked == true) {
      this.formUser = false;
    }
  }
}