
let extensions = {}

export function addExtension(key, item){
  if(!extensions[key]){
    extensions[key] = [];
  }
  extensions[key].push(item);
}

export function getExtensions(key){
  return extensions[key] || [];
}