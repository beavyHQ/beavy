export default new Promise(resolve => {
  require.ensure([], () => {
    const ProseMirror = require('react-prosemirror').default
    require('prosemirror/src/parse/markdown')
    require('prosemirror/src/serialize/markdown')
    require('prosemirror/src/menu/menubar')
    resolve(ProseMirror)
  })
})
