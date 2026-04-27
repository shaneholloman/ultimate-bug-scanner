import DOMPurify from "dompurify";

type Article = {
  title: string;
  html: string;
};

export function ArticlePreview({ article }: { article: Article }) {
  return (
    <article>
      <h1>{article.title}</h1>
      <section
        dangerouslySetInnerHTML={{
          __html: DOMPurify.sanitize(article.html),
        }}
      />
    </article>
  );
}
