import { useCallback, useEffect, useRef, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";

import { Button, Icons, LoadingSpinner } from "@/components";
import { FOOTER_ID } from "@/constants";
import { useTranslation } from "@/i18n";

import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;

type PdfViewerProps = {
  pdfUrl: string;
};

const INITIAL_SCALE = 1.0;
const MINIMUM_ZOOM_LEVEL = 0.5;
const MAXIMUM_ZOOM_LEVEL = 3.0;
const ZOOM_FACTOR = 0.25;
const MINIMUM_PDF_HEIGHT = 300;

export const PdfViewer = ({ pdfUrl }: PdfViewerProps) => {
  const [numPages, setNumPages] = useState<number>(0);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [documentWidth, setDocumentWidth] = useState<number>(0);
  const [documentHeight, setDocumentHeight] = useState<number>(0);
  const [pageScale, setPageScale] = useState<number>(INITIAL_SCALE);
  const [zoomFactor, setZoomFactor] = useState<number>(INITIAL_SCALE);
  const [pageActualWidth, setPageActualWidth] = useState<number>(0);

  const { t } = useTranslation();

  const documentRef = useRef<HTMLDivElement>(null);
  const zoomButtonsRef = useRef<HTMLDivElement>(null);
  const paginationButtonsRef = useRef<HTMLDivElement>(null);

  const onPageRenderSuccess = useCallback(
    (page: { width: number }) => {
      if (pageNumber === 1 && !pageActualWidth) {
        setPageActualWidth(page.width);
      }
    },
    [pageNumber, pageActualWidth],
  );

  const onDocumentLoadSuccess = useCallback(({ numPages }: { numPages: number }) => {
    setNumPages(numPages);
    setPageNumber(1);

    setZoomFactor(INITIAL_SCALE);
    setPageActualWidth(0);
  }, []);

  const previousPage = () => {
    return setPageNumber((prevPageNumber) => {
      return prevPageNumber - 1;
    });
  };

  const nextPage = () => {
    return setPageNumber((prevPageNumber) => {
      return prevPageNumber + 1;
    });
  };

  const zoomIn = () => {
    setZoomFactor((prev) => {
      return Math.min(prev + ZOOM_FACTOR, MAXIMUM_ZOOM_LEVEL);
    });
  };

  const zoomOut = () => {
    setZoomFactor((prev) => {
      return Math.max(prev - ZOOM_FACTOR, MINIMUM_ZOOM_LEVEL);
    });
  };

  const resetZoom = () => {
    setZoomFactor(INITIAL_SCALE);
  };

  useEffect(() => {
    const handleResize = () => {
      if (documentRef.current) {
        const containerRect = documentRef.current.getBoundingClientRect();
        setDocumentWidth(containerRect.width);

        const footerHeight =
          document.querySelector(`#${FOOTER_ID}`)?.getBoundingClientRect().height ?? 0; // Mark as complete button height.

        const viewportHeight = window.innerHeight; // Full screen size.

        const containerTop = containerRect.top; // Distance from top of the viewport to the top of the Document (header + zoom buttons).

        const paginationHeight = paginationButtonsRef.current?.getBoundingClientRect().height
          ? paginationButtonsRef.current?.getBoundingClientRect().height + 16 // Gap of document.
          : 0; // Pagination height + margin top.

        const CONTAINER_PADDING = 16; // Container bottom padding.

        const availableHeight =
          viewportHeight - containerTop - paginationHeight - footerHeight - CONTAINER_PADDING;

        const finalDocumentHeight = Math.max(availableHeight, MINIMUM_PDF_HEIGHT);

        setDocumentHeight(finalDocumentHeight);
      }
    };

    handleResize();

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, [numPages]);

  useEffect(() => {
    if (documentWidth > 0 && pageActualWidth > 0) {
      const initialFitScale = documentWidth / pageActualWidth;
      setPageScale(initialFitScale * zoomFactor);
    } else if (documentWidth > 0 && pageActualWidth === 0) {
      setPageScale(zoomFactor);
    }
  }, [documentWidth, zoomFactor, pageActualWidth]);

  return (
    <div className="flex flex-col items-center gap-4">
      <div
        className="flex w-full justify-between rounded-lg bg-background-brand-invert"
        ref={zoomButtonsRef}
      >
        <Button onClick={resetZoom} variant="iconPlainText">
          {t("pdfViewer.buttons.reset")}
        </Button>

        <div className="flex gap-4">
          <Button
            disabled={zoomFactor <= MINIMUM_ZOOM_LEVEL}
            onClick={zoomOut}
            variant="iconPlainText"
          >
            <Icons.MagnifyingGlassMinus className="size-6" />
          </Button>

          <Button
            disabled={zoomFactor >= MAXIMUM_ZOOM_LEVEL}
            onClick={zoomIn}
            variant="iconPlainText"
          >
            <Icons.MagnifyingGlassPlus className="size-6" />
          </Button>
        </div>
      </div>

      <div
        className="w-full overflow-auto rounded-lg border border-border-neutral-default"
        ref={documentRef}
        style={{ height: documentHeight > 0 ? `${documentHeight}px` : `${MINIMUM_PDF_HEIGHT}px` }}
      >
        {documentWidth > 0 && (
          <Document
            error={<div className="p-4 text-center text-red-600">{t("pdfViewer.error")}</div>}
            file={pdfUrl}
            loading={<LoadingSpinner />}
            noData={<div className="p-4 text-center">{t("pdfViewer.noData")}</div>}
            onLoadSuccess={onDocumentLoadSuccess}
          >
            <Page
              loading={<LoadingSpinner />}
              onRenderSuccess={onPageRenderSuccess}
              pageNumber={pageNumber}
              scale={pageScale}
            />
          </Document>
        )}
      </div>

      {numPages > 1 && (
        <div className="flex w-full items-center justify-between gap-2" ref={paginationButtonsRef}>
          <Button disabled={pageNumber <= 1} onClick={previousPage} variant="outlined">
            {t("pdfViewer.buttons.back")}
          </Button>

          <span className="p-2 text-lg font-medium">
            {pageNumber}/{numPages}
          </span>

          <Button disabled={pageNumber >= numPages} onClick={nextPage} variant="outlined">
            {t("pdfViewer.buttons.next")}
          </Button>
        </div>
      )}
    </div>
  );
};
