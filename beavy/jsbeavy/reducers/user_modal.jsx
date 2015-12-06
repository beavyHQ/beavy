
import { addNamedExtension } from 'config/extensions'
import { OPEN_LOGIN, OPEN_REGISTER, CLOSE_MODAL } from 'actions/user_modal'

// normally this would be imported from /constants, but in trying to keep
// this starter kit as easy to customize as possibility we'll just define
// the constant here.
export const USER_MODAL = 'USER_MODAL'

function ModalStateReducer (state = null, action) {
  switch (action.type) {
    case OPEN_LOGIN:
      return 'LOGIN'
    case OPEN_REGISTER:
      return 'REGISTER'
    case CLOSE_MODAL:
      return ''
    default:
      return state
  }
}

addNamedExtension('reducers', USER_MODAL, ModalStateReducer)
