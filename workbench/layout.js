'use strict';

// Cell boundaries use the same rounding for the reference canvas and the actual video.
const SpriteLayout = {
  actions: {idle:'待机循环', walk:'原地步行', run:'原地跑步', attack:'攻击 / 技能', vfx:'独立特效'},
  handoffKey: 'sprite-studio-layout',
  valid(layout) {
    if (!layout || layout.version !== 1) return false;
    const {cols,rows,width,height,color,baseline,action,cells} = layout;
    const inRange = (value,min,max) => Number.isInteger(value) && value >= min && value <= max;
    if (!inRange(cols,1,8) || !inRange(rows,1,8) || !inRange(width,1,8000) || !inRange(height,1,8000) ||
        typeof color !== 'string' || !/^#[0-9a-f]{6}$/i.test(color) || !Number.isFinite(baseline) ||
        baseline < 0 || baseline > 1 || !Object.hasOwn(this.actions,action) ||
        !Array.isArray(cells) || !cells.length || cells.length > rows * cols) return false;
    const seen = new Set();
    for (const cell of cells) {
      if (!cell || !inRange(cell.col,0,cols-1) || !inRange(cell.row,0,rows-1) ||
          typeof cell.name !== 'string' || !cell.name.trim() || cell.name.length > 160 ||
          !Object.hasOwn(this.actions,cell.action || action)) return false;
      const id = cell.row * cols + cell.col;
      if (seen.has(id)) return false;
      seen.add(id);
    }
    return true;
  },
  cellRect(row, col, rows, cols, width, height) {
    const x = Math.round(col * width / cols);
    const y = Math.round(row * height / rows);
    return {x, y, w: Math.round((col + 1) * width / cols) - x, h: Math.round((row + 1) * height / rows) - y};
  },
  regions(layout, width, height) {
    return layout.cells.map(cell => {
      const rect = this.cellRect(cell.row, cell.col, layout.rows, layout.cols, width, height);
      const anchor = cell.action === 'vfx' || layout.action === 'vfx' ? null : {
        x: Math.round((cell.col + 0.5) * width / layout.cols),
        y: Math.round((cell.row + layout.baseline) * height / layout.rows)
      };
      return {...rect, name:cell.name, action:cell.action || layout.action,
        cell:{row:cell.row, col:cell.col}, anchor};
    });
  }
};
