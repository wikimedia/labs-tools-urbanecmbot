select page_title,
concat(
	"{{Překlad|",
	left(replace(rev_comment, "Vytvořeno překladem stránky „[[:", ""), 2), "|",
	replace(replace(replace(rev_comment, substring_index(rev_comment, "|", 1), ""), "|", ""), "]]“", ""), "|",
	SUBSTRING_INDEX(replace(substr(replace(rev_comment, "Vytvořeno překladem stránky „[[:", ""), 4), "Special:Redirect/revision/", ""), "|", 1), "}}"
) as template
from change_tag
join revision on ct_rev_id=rev_id
join page on rev_page=page_id
where ct_tag="contenttranslation"
and ct_rev_id is not null
and rev_page not in
(select tl_from from templatelinks where tl_title="Překlad")
and page_namespace=0
and rev_parent_id=0
and rev_page not in (select tl_from from templatelinks where tl_title like "Rozcestník%");
