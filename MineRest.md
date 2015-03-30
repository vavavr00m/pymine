## API Documentation ##

See the `apidocs` directory in the pymine distribution.

## Glossary ##

  * _cid_ = commentId, integer > 0
  * _iid_ = itemId, integer > 0
  * _rid_ = relationId, integer > 0
  * _rvsn_ = relationVersion, integer > 0
  * _tid_ = tagId, integer > 0
  * _vid_ = vurlId, integer > 0

## API Request Formats ##

  * `json`
  * `xml`
  * `raw`
  * `rdr`

## API Query Envelopes ##

  * `_method=DELETE`: applies only to HTTP 'POST' calls, to fake a HTTP 'DELETE'
  * `_filedata=FOO`: applies only to HTTP 'POST' calls for file-save or file-update, to fake RFC1867 file upload.

## API Result Envelopes ##

  * `exit`
  * `status`
  * `result` (optional)
  * `prevurl` (optional, paged-calls only)
  * `thisurl` (optional, paged-calls only)
  * `nexturl` (optional, paged-calls only)
  * `count` (optional, paged-calls only)
  * `span` (optional, paged-calls only)
  * `page` (optional, paged-calls only)