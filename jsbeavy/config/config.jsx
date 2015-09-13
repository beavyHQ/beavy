// IMPORTANT NOTE:
// Don't forget to add the key you want to see
// to _both_ the dictionary (with its fallback)
// _and_ to the string in the end
export default Object.assign({
  'MODULES': [],
  'FRONTEND': 'minima',
  'USERS_URL': '/u'
}, require("json!grep?MODULES,FRONTEND,USERS_URL!yaml!../../config.yml"))
