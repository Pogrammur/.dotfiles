function Colors(color)
    color = color or 'tokyonight'
    vim.cmd.colorscheme(color)

    vim.api.nvim_set_hl(0, 'Normal', {bg = 'none'})
    vim.api.nvim_set_hl(0, 'NormalFloat', {bg = 'none' })

end

return {
    {
    'folke/tokyonight.nvim',
	lazy= false,
	priority = 999,
	config = function()
        require('tokyonight').setup({
            disable_background = true
        })

		vim.cmd('colorscheme tokyonight')

        Colors()
	end
},

	'EdenEast/nightfox.nvim',

}
