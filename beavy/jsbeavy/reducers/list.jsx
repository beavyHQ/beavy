import { addNamedExtension } from 'config/extensions'
import { LIST_UPDATED } from 'actions/list'

const list = (state = {}, action) => {
  if (action.type === LIST_UPDATED) {
    return action.response.entities.list[action.repsonse.result]
  }
  return state
}

addNamedExtension('reducers', 'list', list)

