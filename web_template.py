TEMPLATE = '''<!--
The request to this GraphQL server provided the header "Accept: text/html"
and as a result has been presented GraphiQL - an in-browser IDE for
exploring GraphQL.
If you wish to receive JSON, provide the header "Accept: application/json" or
add "&raw" to the end of the URL within a browser.
-->
<!DOCTYPE html>
<html>
<head>
  <style>
    html, body {
      height: 100%;
      margin: 0;
      overflow: hidden;
      width: 100%;
    }
  </style>
  <meta name="referrer" content="no-referrer">
  <link href="//cdn.jsdelivr.net/graphiql/{{graphiql_version}}/graphiql.css" rel="stylesheet" />
  <script src="//cdn.jsdelivr.net/fetch/0.9.0/fetch.min.js"></script>
  <script src="//cdn.jsdelivr.net/react/15.0.0/react.min.js"></script>
  <script src="//cdn.jsdelivr.net/react/15.0.0/react-dom.min.js"></script>
  <script src="//cdn.jsdelivr.net/graphiql/{{graphiql_version}}/graphiql.min.js"></script>
</head>
<body>
  <script>
    // Collect the URL parameters
    var parameters = {};
    window.location.search.substr(1).split('&').forEach(function (entry) {
      var eq = entry.indexOf('=');
      if (eq >= 0) {
        parameters[decodeURIComponent(entry.slice(0, eq))] =
          decodeURIComponent(entry.slice(eq + 1));
      }
    });

    // Produce a Location query string from a parameter object.
    function locationQuery(params) {
      return '?' + Object.keys(params).map(function (key) {
        return encodeURIComponent(key) + '=' +
          encodeURIComponent(params[key]);
      }).join('&');
    }

    // Derive a fetch URL from the current URL, sans the GraphQL parameters.
    var graphqlParamNames = {
      query: true,
      variables: true,
      operationName: true
    };

    var otherParams = {};
    for (var k in parameters) {
      if (parameters.hasOwnProperty(k) && graphqlParamNames[k] !== true) {
        otherParams[k] = parameters[k];
      }
    }
    var fetchURL = locationQuery(otherParams);

    // Defines a GraphQL fetcher using the fetch API.
    function graphQLFetcher(graphQLParams) {
      return fetch(fetchURL, {
        method: 'post',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(graphQLParams),
        credentials: 'include',
      }).then(function (response) {
        return response.text();
      }).then(function (responseBody) {
        try {
          return JSON.parse(responseBody);
        } catch (error) {
          return responseBody;
        }
      });
    }

    // When the query and variables string is edited, update the URL bar so
    // that it can be easily shared.
    function onEditQuery(newQuery) {
      parameters.query = newQuery;
      updateURL();
    }

    function onEditVariables(newVariables) {
      parameters.variables = newVariables;
      updateURL();
    }

    function onEditOperationName(newOperationName) {
      parameters.operationName = newOperationName;
      updateURL();
    }

    function updateURL() {
      history.replaceState(null, null, locationQuery(parameters));
    }

    // Render <GraphiQL /> into the body.
    ReactDOM.render(
      React.createElement(GraphiQL, {
        fetcher: graphQLFetcher,
        onEditQuery: onEditQuery,
        onEditVariables: onEditVariables,
        onEditOperationName: onEditOperationName,
        query: {{query|tojson}},
        response: {{result|tojson}},
        variables: {{variables|tojson}},
        operationName: {{operation_name|tojson}},
      }),
      document.body
    );
    
    
    var pretty_tag = document.querySelector("a[title='Prettify Query']");
    function copyCURL() {
        document.querySelector('input').value = 'curl -X POST ' + window.location.href.replace('&operationName=null', '').replace(/([\?|=|\(|\)])/g, '\\\$1');
        document.querySelector('input').select();document.execCommand('Copy');
    }
    
    var input_tag = document.createElement('input');
    pretty_tag.after(input_tag);
    input_tag.outerHTML = '<input style="width: 50%;" value="' + window.location.href +'">';

    var curl_button_tag = document.createElement('a');
    pretty_tag.after(curl_button_tag);
    curl_button_tag.outerHTML = '<a class="toolbar-button" title="get_curl" onclick="copyCURL();">Copy cURL</a>';
    
    var origin_button_tag = document.createElement('a');
    pretty_tag.after(origin_button_tag);
    origin_button_tag.outerHTML = '<a class="toolbar-button" title="origin" onclick="document.querySelector(\\'input\\').value = decodeURIComponent(window.location.href).split(\\'query=\\')[1].replace(\\'&operationName=null\\', \\'\\');document.querySelector(\\'input\\').select();document.execCommand(\\'Copy\\');">Copy Origin String</a>';
  </script>
</body>
</html>'''