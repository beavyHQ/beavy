// IMPORTANT NOTE:
// Don't forget to add the key you want to see
// to _both_ the dictionary (with its fallback)
// _and_ to the string in the end
export default Object.assign({
  'MODULES': [],
  'FRONTEND': 'minima',
  'USERS_URL': '/u',
  'SECURITY_REGISTERABLE': true
}, require("json!grep?MODULES,SECURITY_REGISTERABLE,FRONTEND,USERS_URL!yaml!../../config.yml"))
