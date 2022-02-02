# Deoplete Shortcut (formerly Clubhouse) plugin

Completes story numbers from Shortcut in git commit messages

## Configuration

The following are configuration options you can set in your `.vimrc` file:

### Query

    let g:deoplete#sources#clubhouse#query = '<query>'

I set mine to `'is:story owner:<my username>'`

### API Token File

This needs to be the absolute path to a file containing your Clubhouse API token (you can find this in Settings > API Tokens)

    let g:deoplete#sources#shortcut#apitokenfile = '/Users/<username>/.clubhouse'