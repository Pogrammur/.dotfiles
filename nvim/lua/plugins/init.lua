return {
    {
        'nvim-lua/plenary.nvim',
    },
    {
        'folke/trouble.nvim',
        config = function()
            require('trouble').setup {
                icons = false,
            }
        end
    },

    'eandrju/cellular-automaton.nvim'

}

