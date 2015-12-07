// IMPORTANT NOTE:
// Don't forget to add the key you want to see
// to _both_ the dictionary (with its fallback)
// _and_ to the string in the end
export default Object.assign({
  'MODULES': [],
  'NAME': 'Nullable',
  'FRONTEND': 'minima',
  'USERS_URL': '/u',
  'HOME_URL': '/hello',
  'ACCOUNT_URL': '/account',
  'SECURITY_REGISTERABLE': true
}, require('json!grep?MODULES,HOME_URL,NAME,ACCOUNT_URL,SECURITY_REGISTERABLE,FRONTEND,USERS_URL!yaml!../../../config.yml'))
