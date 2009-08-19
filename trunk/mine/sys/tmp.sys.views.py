## rest: GET /export
## function: mine_export
## declared args: 
def mine_export(request, *args, **kwargs):
    raise Http404('backend mine_export for GET /export is not yet implemented') # TO BE DONE
    return render_to_response('mine-export.html')

## rest: GET /import
## function: mine_import
## declared args: 
def mine_import(request, *args, **kwargs):
    raise Http404('backend mine_import for GET /import is not yet implemented') # TO BE DONE
    return render_to_response('mine-import.html')

## rest: GET /cleanup
## function: mine_cleanup
## declared args: 
def mine_cleanup(request, *args, **kwargs):
    raise Http404('backend mine_cleanup for GET /cleanup is not yet implemented') # TO BE DONE
    return render_to_response('mine-cleanup.html')

