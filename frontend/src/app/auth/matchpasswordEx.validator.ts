import { AbstractControl, ValidationErrors, ValidatorFn } from "@angular/forms";


  export const matchpasswordEx: ValidatorFn = (control: AbstractControl):ValidationErrors|null =>{

     let password = control.get('passwordEx');
     let confirmpassword = control.get('confirmPasswordEx');
     if(password && confirmpassword && password?.value != confirmpassword?.value){
        return {
            passwordmatcherror : true }
     }
    return null; 
   }