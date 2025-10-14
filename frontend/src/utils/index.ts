export const hasLowerCase = (str: string) => /[a-z]/.test(str);
export const hasUpperCase = (str: string) => /[A-Z]/.test(str);
export const hasNumber = (str: string) => /\d/.test(str);
export const hasSpecialCharacter = (str: string) => /[!@#$%^&*(),.?":{}|<>]/.test(str);
export const hasMinLength = (str: string, minLength: number) => str.length >= minLength;
