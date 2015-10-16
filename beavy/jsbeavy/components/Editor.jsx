

export default new Promise(resolve => {
  require.ensure([], () => {
    const ProseMirror = require('react-prosemirror');
    require('prosemirror/src/parse/markdown');
    require('prosemirror/src/menu/inlinemenu');
    require('prosemirror/src/menu/buttonmenu');
    resolve(ProseMirror);
  });
});
