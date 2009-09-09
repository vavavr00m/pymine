#!/bin/sh


boilerplate() {
cat <<EOF
<LI><A HREF="/admin">django administration</A></LI>
<p/>

<LI><A HREF="/">mine root</A></LI>
<p/>

<LI><A HREF="/api">mine api root</A></LI>
<LI><A HREF="/doc">mine doc root</A></LI>
<LI><A HREF="/get">mine get root</A></LI>
<LI><A HREF="/pub">mine pub root</A></LI>
<LI><A HREF="/sys">mine sys root</A></LI>
<LI><A HREF="/ui">mine ui root</A></LI>
<p/>

<LI><A HREF="/ui/version.html">version</A></LI>
<p/>

<LI><A HREF="/ui/create-comment/1.html">create-comment ON ITEM 1</A></LI>
<LI><A HREF="/ui/create-item.html">create-item</A></LI>
<LI><A HREF="/ui/create-relation.html">create-relation</A></LI>
<LI><A HREF="/ui/create-tag.html">create-tag</A></LI>
<p/>

<LI><A HREF="/ui/delete-comment/1.html">delete-comment 1</A></LI>
<LI><A HREF="/ui/delete-item/1.html">delete-item 1</A></LI>
<LI><A HREF="/ui/delete-relation/1.html">delete-relation 1</A></LI>
<LI><A HREF="/ui/delete-tag/1.html">delete-tag 1</A></LI>
<p/>

<LI><A HREF="/ui/list-comments/0.html">list-comments ON ALL ITEMS</A></LI>
<LI><A HREF="/ui/list-comments/1.html">list-comments ON ITEM 1</A></LI>
<LI><A HREF="/ui/list-items.html">list-items</A></LI>
<LI><A HREF="/ui/list-relations.html">list-relations</A></LI>
<LI><A HREF="/ui/list-tags.html">list-tags</A></LI>
<p/>

<LI><A HREF="/ui/read-comment/1.html">read-comment 1</A></LI>
<LI><A HREF="/ui/read-item/1.html">read-item 1</A></LI>
<LI><A HREF="/ui/read-relation/1.html">read-relation 1</A></LI>
<LI><A HREF="/ui/read-tag/1.html">read-tag 1</A></LI>
<p/>

<LI><A HREF="/ui/update-comment/1.html">update-comment 1</A></LI>
<LI><A HREF="/ui/update-item/1.html">update-item 1</A></LI>
<LI><A HREF="/ui/update-relation/1.html">update-relation 1</A></LI>
<LI><A HREF="/ui/update-tag/1.html">update-tag 1</A></LI>
<p/>

<LI><A HREF="/ui/read-registry.html">read-registry</A></LI>
<LI><A HREF="/ui/update-registry.html">update-registry</A></LI>
<p/>
EOF
}

for i in *.html
do
    echo "<h2>you are looking at $i</h2>" > $i
    boilerplate >> $i
done

