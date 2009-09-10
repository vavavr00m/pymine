for i in api archive doc get mine pub ui
do
cat > root-$i.html <<EOF
{% extends 'base-page.html' %}
{% block title %}$i root{% endblock %}
{% block content %}
you are looking at root-$i.html
<P>
{% include 'developer-boilerplate.html' %}
{% endblock %}
EOF
done
