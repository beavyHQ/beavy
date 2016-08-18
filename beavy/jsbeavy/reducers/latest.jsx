import { addNamedExtension } from 'config/extensions'
import paginate from 'reducers/paginate'
import { LATEST_SUCCESS, LATEST_FAILURE, LATEST_REQUEST } from 'actions/latest'

export const LATEST = 'latest'

addNamedExtension('reducers', LATEST, paginate({
  mapActionToKey: x => LATEST,
  types: [LATEST_REQUEST, LATEST_SUCCESS, LATEST_FAILURE]
}))

