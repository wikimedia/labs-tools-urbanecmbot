SELECT
  p1.page_namespace,
  p1.page_title
FROM page AS p1
WHERE p1.page_title NOT LIKE "%/%"
AND p1.page_namespace NOT IN (0,2,3,4,6,8,9,10,12,14,16,18,100,102,104,108, 118, 710, 828, 2300, 2600)
AND CASE WHEN p1.page_namespace = 1
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 0
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 5
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 4
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 7
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 6
                   AND p1.page_title = p2.page_title)
  AND NOT EXISTS (SELECT
                    1
                  FROM commonswiki_p.page AS p2
                  WHERE p2.page_namespace = 6
                  AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 11
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 10
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 13
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 12
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 15
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 14
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 17
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 16
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 101
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 100
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 109
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 108
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 119
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 118
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 711
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 710
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 829
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 828
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND CASE WHEN p1.page_namespace = 2301
  THEN NOT EXISTS (SELECT
                     1
                   FROM page AS p2
                   WHERE p2.page_namespace = 2300
                   AND p1.page_title = p2.page_title)
  ELSE 1 END
AND p1.page_id NOT IN (SELECT
                         page_id
                       FROM page
                       JOIN templatelinks
                       ON page_id = tl_from
                       WHERE tl_title="G8-exempt"
                       AND tl_namespace = 10)
AND p1.page_id NOT IN (SELECT
                         page_id
                       FROM page
                       JOIN templatelinks
                       ON page_id = tl_from
                       WHERE tl_title="Rtd"
                       AND tl_namespace = 10);
