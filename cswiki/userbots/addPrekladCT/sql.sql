select page_title,
concat(
	"{{Překlad|",
	left(replace(comment_text, "Vytvořeno překladem stránky „[[:", ""), 2), "|",
	replace(replace(replace(comment_text, substring_index(comment_text, "|", 1), ""), "|", ""), "]]“", ""), "|",
	SUBSTRING_INDEX(replace(substr(replace(comment_text, "Vytvořeno překladem stránky „[[:", ""), 4), "Special:Redirect/revision/", ""), "|", 1), "}}"
) as template
from change_tag
join revision on ct_rev_id=rev_id
join page on rev_page=page_id
join comment on rev_comment_id=comment_id
where ct_tag_id in (select ctd_id from change_tag_def where ctd_name in ("contenttranslation", "contenttranslation-v2"))
and ct_rev_id is not null
and rev_page not in
(select tl_from from templatelinks where tl_title="Překlad")
and page_namespace=0
/*and rev_parent_id=0*/
and rev_page not in (select tl_from from templatelinks where tl_title like "Rozcestník%")
and left(replace(comment_text, "Vytvořeno překladem stránky „[[:", ""), 2)!="cs"
and page_is_redirect=0;
