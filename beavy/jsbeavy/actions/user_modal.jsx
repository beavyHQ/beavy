/*
 * action types
 */

export const OPEN_LOGIN = 'OPEN_LOGIN';
export const OPEN_REGISTER = 'OPEN_REGISTER';
export const CLOSE_MODAL = 'USER_MODAL_CLOSED';
// export const CLOSE_LOGIN = 'CLOSE_LOGIN';
// export const CLOSE_REGISTER = 'OPEN_REGISTER';


export function openLogin() {
  return { type: OPEN_LOGIN };
}

export function openRegister() {
  return { type: OPEN_REGISTER };
}

export function closeModal() {
  return { type: CLOSE_MODAL };
}
